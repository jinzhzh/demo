/** Node：迷你编排域模块。 */
export class Node {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createNode = (data={}) => new Node(data);
