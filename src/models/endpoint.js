/** Endpoint：迷你编排域模块。 */
export class Endpoint {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createEndpoint = (data={}) => new Endpoint(data);
