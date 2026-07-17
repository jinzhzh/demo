/** ScaleCommand：迷你编排域模块。 */
export class ScaleCommand {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createScaleCommand = (data={}) => new ScaleCommand(data);
