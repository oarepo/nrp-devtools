import {
  createSearchAppInit
} from '@js/oarepo_ui/search'

const appName = '{{cookiecutter.name}}.Search'

createSearchAppInit({
  defaultComponentOverrides: {
    [`${appName}.ResultsList.item`]: "{{cookiecutter.name}}/search/ResultListItem",
  },
})
