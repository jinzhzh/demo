/** HealthPolicy：迷你编排域模块。 */
export class HealthPolicy {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createHealthPolicy = (data={}) => new HealthPolicy(data);
