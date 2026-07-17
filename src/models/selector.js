/** Selector：迷你编排域模块。 */
export class Selector {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createSelector = (data={}) => new Selector(data);
