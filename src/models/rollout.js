/** Rollout：迷你编排域模块。 */
export class Rollout {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRollout = (data={}) => new Rollout(data);
