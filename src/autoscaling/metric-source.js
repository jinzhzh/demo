/** MetricSource：迷你编排域模块。 */
export class MetricSource {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createMetricSource = (data={}) => new MetricSource(data);
