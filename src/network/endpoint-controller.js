/** EndpointController：迷你编排域模块。 */
export class EndpointController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createEndpointController = (data={}) => new EndpointController(data);
