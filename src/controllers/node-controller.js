/** NodeController：迷你编排域模块。 */
export class NodeController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createNodeController = (data={}) => new NodeController(data);
