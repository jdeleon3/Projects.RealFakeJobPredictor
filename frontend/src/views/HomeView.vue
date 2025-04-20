<script setup>

</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-center mt-10">Welcome to FakeFinder</h1>
    <div class="text-center">
      <p class="text-center mt-4">The place to see if a Job posting is Fake or Real using Machine Learning.</p>
      <p class="pb-4">
        Enter a Freelancer.com job posting URL, or fill out a the form to test the model.
      </p>      
      <hr />
      <div>
        <div class="mt-8">

          <label class="inline-flex items-center cursor-pointer">
            <input type="checkbox" id="useUrl" v-model="urlToggle" class="hidden" aria-label="Import data?" />

            <div :class="['relative w-11 h-6 rounded-full transition-colors',
              urlToggle ? 'bg-blue-600' : 'bg-gray-300']"
              @focus="$event.target.classList.add('ring-2', 'ring-blue-500')"
              @blur="$event.target.classList.remove('ring-2', 'ring-blue-500')">
              <div :class="['absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-all duration-300 ease-in-out',
                urlToggle ? 'transform translate-x-5' : '']">
              </div>
            </div>
            <span class="ml-3 text-xl"><strong>Import data?</strong></span>
          </label>


        </div>
        <div v-if="urlToggle && job.description == ''" class="flex flex-col">
          <div><input type="text" name="jobUrl" id="jobUrl" v-model="url" placeholder="Enter Job URL"
            class="mt-4 p-2 border border-gray-300 rounded-md w-full" /></div>
            <p class="my-4 font-bold font-">OR</p>
            <div>
          <textarea name="jobimportstr" id="jobimportstr" class="mt-4 p-2 border border-gray-300 rounded-md w-full h-20 md:h-40 lg:h-60" v-model="importstr" placeholder="Enter job post data in JSON format" />
            </div>
            <div>
                <button @click="importData()" class="mx-4 mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-75 disabled:bg-slate-300" :disabled="url ==  '' && importstr == ''">Import</button>
            </div>
          
            
        </div>
        
        <div v-if="!urlToggle || job.description != ''">
          <input type="text" name="jobTitle" id="jobTitle" v-model="job.title" placeholder="Enter Job Title"
            class="mt-4 p-2 border border-gray-300 rounded-md w-full" />
          <textarea name="jobDescription" id="jobDescription" v-model="job.description"
            placeholder="Enter Job Description" class="mt-4 p-2 border border-gray-300 rounded-md w-full h-20 md:h-40 lg:h-60"></textarea>
          
            <div>
              <button @click="analyzeJob()" :disabled="job.description == ''"
                class=" mx-4 mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-75 disabled:bg-slate-300">Submit</button>
              <button @click="clearJobData()"
                class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Clear</button>
            </div>

        </div>
        <div v-if="haveJobAnalysis" class="mt-4">
          <h2 class="font-bold text-2xl">Results</h2>
          <div class="mt-4">
            <p><strong>Is Job Real?:</strong>&nbsp; &nbsp;{{ isRealFake }} </p>
            <p><strong>Keywords:</strong>&nbsp; &nbsp;{{ jobKeywords }} </p>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
  const urlToggle = ref(false);
  const url = ref('');
  const importstr = ref('');
  const isRealFake = ref(false);
  const jobKeywords = ref([]);
  const haveJobAnalysis = ref(false);
  const job = ref({
    title: '',
    description: ''
  });

  var importData = async () => {
    if(url.value != ''){
      const response = await fetch(`api/getjobpost`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "url": url.value })
      });
      const data = await response.json();
      console.log(data);
      job.value = {
        title: data.title,
        description: data.description
      };
      haveJobAnalysis.value = false;
    }
    else if(importstr.value != ''){
      try {
        const parsedData = JSON.parse(importstr.value);
        job.value = {
          title: parsedData.title,
          description: parsedData.description
        };
      } catch (error) {
        console.error('Invalid JSON format:', error);
        alert('Invalid JSON format. Please check your input.');
      }
      haveJobAnalysis.value = false;
    }
    
  };

  var analyzeJob = async () => {
    const response = await fetch(`api/evaluatejobpost`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(job.value)
    });
    const data = await response.json();
    console.log(data);
    isRealFake.value = data.is_real;
    haveJobAnalysis.value = true;
    console.log(data);
  };

  var clearJobData = () => {
    job.value = {
      title: '',
      description: ''
    };
    url.value = '';
    importstr.value = '';
    isRealFake.value = false;
    jobKeywords.value = [];
    haveJobAnalysis.value = false;
  };

</script>