/** LoadBalancer：迷你编排域模块。 */
export class LoadBalancer {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createLoadBalancer = (data={}) => new LoadBalancer(data);
