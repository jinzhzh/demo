/** ServiceController：迷你编排域模块。 */
export class ServiceController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createServiceController = (data={}) => new ServiceController(data);
