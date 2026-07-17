/** StartupProbe：迷你编排域模块。 */
export class StartupProbe {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createStartupProbe = (data={}) => new StartupProbe(data);
