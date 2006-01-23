from BaseFormAction import BaseFormAction, registerFormAction
import RedirectTo

def factory(arg):
    """Create a new redirect-to-action action"""
    return RedirectToAction(arg)


class RedirectToAction(BaseFormAction):

    def __call__(self, controller_state):
        action = self.getArg(controller_state)
        action_url = None
        haveAction = False

        context = controller_state.getContext()
        fti = context.getTypeInfo()

        try:
            #action_url = fti.getActionById(action)
            action_url = fti.getActionObject(action).getActionExpression()
            haveAction = True
        except ValueError:
            actions = controller_state.getContext().portal_actions.listFilteredActionsFor(controller_state.getContext())
            # flatten the actions as we don't care where they are
            actions = reduce(lambda x,y,a=actions:  x+a[y], actions.keys(), [])
            for actiondict in actions:
                if actiondict['id'] == action:
                    action_url = actiondict['url'].strip()
                    haveAction = True
                    break

        # (note: action_url may now be an emptry string, but still valid)
        if not haveAction:
            raise ValueError, 'No %s action found for %s' % (action, controller_state.getContext().getId())

        # If we have CMF 1.5, the actual action_url may be hidden behind a method
        # alias. Attempt to resolve this
        try:
            if action_url:
                action_url = fti.queryMethodID(action_url, default = action_url,
                                                           context = context)
        except AttributeError:
            # Don't raise if we don't have CMF 1.5
            pass

        # XXX: Is there a better way to check this?
        if not action_url.startswith('string:'):
            action_url = 'string:%s' % (action_url,)
        return RedirectTo.RedirectTo(action_url)(controller_state)

registerFormAction('redirect_to_action',
                   factory,
                   'Redirect to the action specified in the argument (a TALES expression) for the current context object (e.g. string:view)')
