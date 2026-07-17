/** Timeline：迷你编排域模块。 */
export class Timeline {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createTimeline = (data={}) => new Timeline(data);
