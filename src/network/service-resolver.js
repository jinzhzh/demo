/** ServiceResolver：迷你编排域模块。 */
export class ServiceResolver {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createServiceResolver = (data={}) => new ServiceResolver(data);
