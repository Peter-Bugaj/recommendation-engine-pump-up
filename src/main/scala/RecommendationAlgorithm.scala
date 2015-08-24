package Piotrekoper

import io.prediction.controller.P2LAlgorithm
import io.prediction.controller.Params
import io.prediction.data.storage.BiMap

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.mllib.recommendation.ALS
import org.apache.spark.mllib.recommendation.{Rating => MLlibRating}

import grizzled.slf4j.Logger

import scala.collection.parallel.immutable.ParVector

/**
 * ALgorithm for reading in training data, creating a predictive
 * model, and for executing a query using the help of the model.
 */
class RecommendationAlgorithm()
  extends P2LAlgorithm[PreparedData, ALSModel, Query, PredictedResult] {

  @transient lazy val logger = Logger[this.type]
  def train(sc: SparkContext, data: PreparedData): ALSModel = {

    // Check that no data is missing.
    require(!data.likeEvents.take(1).isEmpty,
      s"likeEvents in PreparedData cannot be empty." +
      " Please check if DataSource generates TrainingData" +
      " and Preprator generates PreparedData correctly.")
    require(!data.users.take(1).isEmpty,
      s"users in PreparedData cannot be empty." +
      " Please check if DataSource generates TrainingData" +
      " and Preprator generates PreparedData correctly.")
    require(!data.posts.take(1).isEmpty,
      s"posts in PreparedData cannot be empty." +
      " Please check if DataSource generates TrainingData" +
      " and Preprator generates PreparedData correctly.")

    // Count the number of likes per post
    // and sort it in descending order.
    val userStringIntMap = BiMap.stringInt(data.users.keys)
    val postStringIntMap = BiMap.stringInt(data.posts.keys)

    val counts = data.likeEvents
      .map { likeEvent =>
        val uindex = userStringIntMap.getOrElse(likeEvent.user, -1)
        val pindex = postStringIntMap.getOrElse(likeEvent.post, -1)

        // For safety, avoid likes that either have no
        // associated post or did not come from any user.
        if (uindex == -1)
          logger.info(s"Couldn't convert nonexistent user ID ${likeEvent.user}"
            + " to Int index.")
        if (pindex == -1)
          logger.info(s"Couldn't convert nonexistent post ID ${likeEvent.post}"
            + " to Int index.")
        (uindex, pindex, likeEvent.post, 1)

      }.filter { case (u, pid, pname, v) =>
        (u != -1) && (pid != -1)

      }.map{
        quad => (quad._3 , quad._4 )

        // Finally sum up the likes per post and sort them
        // by number of likes to get the most liked.
      }.reduceByKey(_ + _).sortBy(pair => pair._2, false);

    // Build the model.
    val ranks = counts.collect()
    val postIdToRankIndex = ranks.indices
      .map(index => (ranks(index)._1, index))
      .sortBy(pair => pair._1);
    new ALSModel(
      ranks = ranks,
      postIdToRankIndex = postIdToRankIndex
    )
  }

  /**
   * Returns a result of posts sorted by most likes, given a
   * query specifying the post ID to start returning the posts
   * from and a limit to the total number of posts to return.
   */
  def predict(model: ALSModel, query: Query): PredictedResult = {

    // Fetch the model parameters.
    val postRanks = model.ranks;

    if (postRanks.take(1).isEmpty) {
      return PredictedResult(
        likeScores = Array()
      );
    }

    // Read the query parameters.
    val lastPostId = query.lastPostId;
    val limit = query.limit;

    // Fetch the last post to get the ID from and the limit if provided
    val postPosition = if (lastPostId == null) 0
      else model.getPostPosition(lastPostId);

    // Compute the range of the data to return.
    val start = if (postPosition == -1) 0 else postPosition;
    val end = if (limit == null) postRanks.length
      else Math.min(start + limit, postRanks.length);

    // Return the most liked posts
    PredictedResult(
      likeScores = postRanks.slice(start, end).
        map{pair => PostScore(pair._1 , pair._2)}
    )
  }
}
