/** Service：迷你编排域模块。 */
export class Service {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createService = (data={}) => new Service(data);
