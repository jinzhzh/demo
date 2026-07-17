/** CommandContext：迷你编排域模块。 */
export class CommandContext {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createCommandContext = (data={}) => new CommandContext(data);
