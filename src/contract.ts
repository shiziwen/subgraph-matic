import {Transfer} from "../generated/Contract/Contract"
import {TransferCounter,} from '../generated/schema'
import {BigInt} from "@graphprotocol/graph-ts";


export function handleTransfer(event: Transfer): void {
  let blocknumber = event.block.number
  let day = (event.block.timestamp / BigInt.fromI32(60 * 60 * 24))

  // Transfer counter total and historical
  let transferCounter = TransferCounter.load('singleton')
  if (transferCounter == null) {
    transferCounter = new TransferCounter('singleton')
    transferCounter.count = 0
    transferCounter.totalTransferred = BigInt.fromI32(0)
  }
  transferCounter.blockNumber = blocknumber
  transferCounter.count = transferCounter.count + 1
  transferCounter.totalTransferred = transferCounter.totalTransferred + event.params.value
  transferCounter.save()
  transferCounter.id = day.toString()
  transferCounter.save()
}