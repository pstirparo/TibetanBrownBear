<template>
  <!-- Display details nicely -->
  <div v-if="!edit" class="entity-details">
    <div class="loading" v-if="loading">
      Loading...
    </div>
    <div v-else>
      <h3>{{entity.name}} <small>{{entity.type}}</small></h3>
      <fields :field="{'type': 'list', 'name': 'labels'}"  :elt="entity" />
      {{entity.description || 'No description'}}
    </div>
    <router-link class="edit btn btn-sm btn-outline-secondary" :to="{name: 'EntityEdit', params: {id: id}}">Edit</router-link>
    <links :object="entity"/>
  </div>

  <!--  Edit form -->
  <!-- yeti-form should use emit instead of an onSaveCallback -->
  <yeti-form :object="entity"
             :fields="entityFields"
             :apiPath="defaultApiPath+id+'/'"
             method='PUT'
             v-on:form-submit='toggleEdit'
             v-else
             />
</template>

<script>
import axios from 'axios'
import YetiForm from '@/components/scaffolding/YetiForm'
import Links from '@/components/Graph/Links'
import Fields from '@/components/helpers/Fields'
import { typeFields } from './EntityFields.js'

export default {
  data () {
    return {
      loading: true,
      entity: {},
      error: {},
      defaultApiPath: `http://localhost:5000/api/entities/`
    }
  },
  props: { id: [Number, String], edit: Boolean },
  components: {
    YetiForm,
    Fields,
    Links
  },
  beforeRouteUpdate (to, from, next) { // how do we test this?
    this.fetchInfo()
    next()
  },
  computed: {
    entityType () {
      if (this.entity.type) {
        let arr = this.entity.type.split('.')
        return arr[arr.length - 1]
      }
    },
    entityFields () {
      return typeFields[this.entityType]
    }
  },
  methods: {
    fetchInfo () {
      axios.get(this.defaultApiPath + this.id)
        .then(response => {
          if (response.status !== 200) {
            this.error = response.data
          } else {
            this.entity = response.data
          }
        })
        .catch(error => { // how do we catch 404 errors?
          this.error = error
        })
        .finally(() => { this.loading = false })
    },
    toggleEdit () {
      this.$router.go(-1)
    }
  },
  mounted () {
    this.fetchInfo()
  }
}
</script>

<style lang="css">
</style>
