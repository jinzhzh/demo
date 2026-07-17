/** ReadinessProbe：迷你编排域模块。 */
export class ReadinessProbe {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReadinessProbe = (data={}) => new ReadinessProbe(data);
