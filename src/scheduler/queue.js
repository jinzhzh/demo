/** Queue：迷你编排域模块。 */
export class Queue {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createQueue = (data={}) => new Queue(data);
