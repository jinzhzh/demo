/** RolloutCommand：迷你编排域模块。 */
export class RolloutCommand {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRolloutCommand = (data={}) => new RolloutCommand(data);
