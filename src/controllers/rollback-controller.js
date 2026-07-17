/** RollbackController：迷你编排域模块。 */
export class RollbackController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRollbackController = (data={}) => new RollbackController(data);
