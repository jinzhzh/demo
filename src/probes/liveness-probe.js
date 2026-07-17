/** LivenessProbe：迷你编排域模块。 */
export class LivenessProbe {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createLivenessProbe = (data={}) => new LivenessProbe(data);
