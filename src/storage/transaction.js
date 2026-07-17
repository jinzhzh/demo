/** Transaction：迷你编排域模块。 */
export class Transaction {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createTransaction = (data={}) => new Transaction(data);
