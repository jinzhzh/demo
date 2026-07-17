/** LabelSet：迷你编排域模块。 */
export class LabelSet {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createLabelSet = (data={}) => new LabelSet(data);
