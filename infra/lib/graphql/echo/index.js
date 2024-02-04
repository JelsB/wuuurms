exports.handler = async function (event, context) {
  console.log('event', event)
  console.log('updating the score of the player based on the event data')
  return 'updated'
}
