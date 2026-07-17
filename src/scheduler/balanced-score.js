/** BalancedScore：迷你编排域模块。 */
export class BalancedScore {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createBalancedScore = (data={}) => new BalancedScore(data);
