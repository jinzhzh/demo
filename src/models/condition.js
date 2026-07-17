/** Condition：迷你编排域模块。 */
export class Condition {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createCondition = (data={}) => new Condition(data);
