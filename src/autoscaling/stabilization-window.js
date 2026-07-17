/** StabilizationWindow：迷你编排域模块。 */
export class StabilizationWindow {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createStabilizationWindow = (data={}) => new StabilizationWindow(data);
