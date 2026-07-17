/** Deployment：迷你编排域模块。 */
export class Deployment {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createDeployment = (data={}) => new Deployment(data);
