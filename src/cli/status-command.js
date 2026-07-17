/** StatusCommand：迷你编排域模块。 */
export class StatusCommand {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createStatusCommand = (data={}) => new StatusCommand(data);
