/** ScalingPolicy：迷你编排域模块。 */
export class ScalingPolicy {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createScalingPolicy = (data={}) => new ScalingPolicy(data);
