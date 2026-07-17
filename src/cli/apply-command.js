/** ApplyCommand：迷你编排域模块。 */
export class ApplyCommand {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createApplyCommand = (data={}) => new ApplyCommand(data);
