/** RolloutController：迷你编排域模块。 */
export class RolloutController {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRolloutController = (data={}) => new RolloutController(data);
