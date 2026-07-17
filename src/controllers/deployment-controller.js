/** DeploymentController：迷你编排域模块。 */
export class DeploymentController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createDeploymentController = (data={}) => new DeploymentController(data);
