import Vue from 'vue'
import Router from 'vue-router'
import ObservableList from '@/components/Observables/ObservableList'

import EntityList from '@/components/Entities/EntityList'
import EntityDetails from '@/components/Entities/EntityDetails'

import IndicatorList from '@/components/Indicators/IndicatorList'
import IndicatorDetails from '@/components/Indicators/IndicatorDetails'

import AdminMain from '@/components/Admin/AdminMain'
import Tags from '@/components/Admin/Tags'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/observables',
      name: 'ObservableList',
      component: ObservableList
    },
    // Entities
    {
      path: '/entities/:type([a-z]+)?',
      name: 'EntityList',
      component: EntityList
    },
    {
      path: '/entities/:id(\\d+)',
      name: 'EntityDetails',
      component: EntityDetails,
      children: [
        {
          name: 'EntityEdit',
          path: 'edit',
          component: EntityDetails
        }
      ]
    },
    // Indicators
    {
      path: '/indicators/:type([a-z]+)?',
      name: 'IndicatorList',
      component: IndicatorList
    },
    {
      path: '/indicators/:id(\\d+)',
      name: 'IndicatorDetails',
      component: IndicatorDetails,
      children: [
        {
          name: 'IndicatorEdit',
          path: 'edit',
          component: IndicatorDetails
        }
      ]
    },
    // Settings
    {
      path: '/admin',
      name: 'AdminMain',
      component: AdminMain,
      children: [
        {
          name: 'Tags',
          path: 'tags',
          component: Tags
        }
      ]
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ],
  mode: 'history'
})