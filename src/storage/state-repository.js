/** StateRepository：迷你编排域模块。 */
export class StateRepository {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createStateRepository = (data={}) => new StateRepository(data);
