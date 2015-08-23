package Piotrekoper

import io.prediction.controller.LServing

/**
 * Class for serving queries.
 */
class Serving
  extends LServing[Query, PredictedResult] {

  override
  def serve(query: Query,
    predictedResults: Seq[PredictedResult]): PredictedResult = {
    predictedResults.head
  }
}
