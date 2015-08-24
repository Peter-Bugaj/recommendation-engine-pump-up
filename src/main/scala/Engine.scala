package Piotrekoper

import io.prediction.controller.IEngineFactory
import io.prediction.controller.Engine

/**
 * Query used for the POST request.
 */
case class Query(

  // The post ID to start returning the most liked posts from.
  lastPostId: String,

  // The limit for the number of posts to retun.
  limit: Integer
) extends Serializable

/**
 * The return result from the POST request.
 */
case class PredictedResult(

  // Array of results containing the post ID and
  // the associated number of likes for the post.
  // The array has the posts sorted in order by
  // most likes.
  likeScores: Array[PostScore]
) extends Serializable

/**
 * The result showing how much likes a post has.
 */
case class PostScore(

  // The post ID.
  postID: String,

  // The number of likes for this post.
  likes: Integer
) extends Serializable

object ProductRankingEngine extends IEngineFactory {
  def apply() = {
    new Engine(
      classOf[DataSource],
      classOf[Preparator],
      Map("als" -> classOf[RecommendationAlgorithm]),
      classOf[Serving])
  }
}
