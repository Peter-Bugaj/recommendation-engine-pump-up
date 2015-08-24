package Piotrekoper

/**
 * The model for the most liked posts.
 */
class ALSModel(

  // The number of likes for each post, ranked in descending order.
  val ranks: Array[(String, Int)],

  // A sorted array mapping a post ID to its index within the ranks
  // array. This structure is sorted such that binary search can be
  // performed on the post ID when a request is sent asking to return
  // likes after a specified 'LastPostId'.
  val postIdToRankIndex: IndexedSeq[(String, Int)]

) extends Serializable {

  /**
   * A binary search algorithm for finding the LastPostId efficiency.
   * For an expected array of 3 million values, the query time is 32
   * milliseconds.
   */
  def binarySearch(ds: IndexedSeq[(String, Int)], key: String): Int = {
    @annotation.tailrec
    def go(low: Int, mid: Int, high: Int): Int = {
      mid match {
        case x if ds(x)._1  == key => ds(x)._2
        case x if high <= low => -1
        case x if ds(x)._1  < key => go(mid + 1, (high - mid + 1) / 2  + mid, high)
        case x if ds(x)._1  > key => go(low, (mid - low) / 2 + low, mid - 1)
      }
    }
    ds.size match {
      case 0 => -1
      case _ => go(0, ds.size / 2, ds.size - 1)
    }
  }

  override def toString = {
    s" ranks: ${ranks}"
  }
}
