/** ProbeRunner：迷你编排域模块。 */
export class ProbeRunner {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createProbeRunner = (data={}) => new ProbeRunner(data);
