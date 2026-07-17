/** Reconciler：迷你编排域模块。 */
export class Reconciler {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createReconciler = (data={}) => new Reconciler(data);
