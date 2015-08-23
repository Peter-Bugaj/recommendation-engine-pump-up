package Piotrekoper

import io.prediction.controller.PPreparator

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD

/**
 * Class for preparing data.
 */
class Preparator
  extends PPreparator[TrainingData, PreparedData] {

  def prepare(sc: SparkContext, trainingData: TrainingData): PreparedData = {
    new PreparedData(
      users = trainingData.users,
      posts = trainingData.posts,
      likeEvents = trainingData.likeEvents)
  }
}

class PreparedData(
  val users: RDD[(String, User)],
  val posts: RDD[(String, Post)],
  val likeEvents: RDD[LikeEvent]
) extends Serializable
