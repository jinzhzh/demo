/** NodeSelectorFilter：迷你编排域模块。 */
export class NodeSelectorFilter {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createNodeSelectorFilter = (data={}) => new NodeSelectorFilter(data);
