package Piotrekoper

import io.prediction.controller.PDataSource
import io.prediction.controller.EmptyEvaluationInfo
import io.prediction.controller.EmptyActualResult
import io.prediction.controller.Params
import io.prediction.data.storage.Event
import io.prediction.data.store.PEventStore

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD

import grizzled.slf4j.Logger

case class DataSourceParams(appName: String) extends Params

/**
 * Class for reading in training data.
 */
class DataSource(val dsp: DataSourceParams)
  extends PDataSource[TrainingData,
      EmptyEvaluationInfo, Query, EmptyActualResult] {

  @transient lazy val logger = Logger[this.type]

  override def readTraining(sc: SparkContext): TrainingData = {

    // Create an RDD of (entityID, User)
    val usersRDD: RDD[(String, User)] = PEventStore.aggregateProperties(
      appName = dsp.appName,
      entityType = "user"
    )(sc).map { case (entityId, properties) =>
      val user = try {

        User()
      } catch {
        case e: Exception => {
          logger.error(s"Failed to get properties ${properties} of" +
            s" user ${entityId}. Exception: ${e}.")
          throw e
        }
      }
      (entityId, user)
    }.cache()

    // Create an RDD of (entityID, Post)
    val postsRDD: RDD[(String, Post)] = PEventStore.aggregateProperties(
      appName = dsp.appName,
      entityType = "post"
    )(sc).map { case (entityId, properties) =>
      val post = try {
        // placeholder for expanding post properties
        Post()
      } catch {
        case e: Exception => {
          logger.error(s"Failed to get properties ${properties} of" +
            s" post ${entityId}. Exception: ${e}.")
          throw e
        }
      }
      (entityId, post)
    }.cache()

    // Get all "user" "like" "post" events
    val likeEventsRDD: RDD[LikeEvent] = PEventStore.find(
      appName = dsp.appName,
      entityType = Some("user"),
      eventNames = Some(List("like")),
      // targetEntityType is optional field of an event.
      targetEntityType = Some(Some("post")))(sc)

      // eventsDb.find() returns RDD[Event]
      .map { event =>
        val likeEvent = try {
          event.event match {
            case "like" => LikeEvent(
              user = event.entityId,
              post = event.targetEntityId.get,
              t = event.eventTime.getMillis)
            case _ => throw new Exception(s"Unexpected event ${event} is read.")
          }
        } catch {
          case e: Exception => {
            logger.error(s"Cannot convert ${event} to LikeEvent." +
              s" Exception: ${e}.")
            throw e
          }
        }
        likeEvent
      }.cache()

    new TrainingData(
      users = usersRDD,
      posts = postsRDD,
      likeEvents = likeEventsRDD
    )
  }
}

case class User()

case class Post()

case class LikeEvent(user: String, post: String, t: Long)

class TrainingData(
  val users: RDD[(String, User)],
  val posts: RDD[(String, Post)],
  val likeEvents: RDD[LikeEvent]
) extends Serializable {
  override def toString = {
    s"users: [${users.count()} (${users.take(2).toList}...)]" +
    s"posts: [${posts.count()} (${posts.take(2).toList}...)]" +
    s"likeEvents: [${likeEvents.count()}] (${likeEvents.take(2).toList}...)"
  }
}
