/** CpuMetric：迷你编排域模块。 */
export class CpuMetric {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createCpuMetric = (data={}) => new CpuMetric(data);
