/** Predicate：迷你编排域模块。 */
export class Predicate {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createPredicate = (data={}) => new Predicate(data);
