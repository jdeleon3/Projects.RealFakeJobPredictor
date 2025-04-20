<template>
  <div>
    <h2 class="font-bold">Project Summary </h2>
    <p>The rise of online job boards has created countless opportunities for job seekers — but it has also opened the door to fraudulent job postings that exploit those searching for work. This project aims to build a machine learning model that can automatically detect fake job postings based on their content and associated metadata. By using a combination of natural language processing (NLP) and structured data analysis, this project seeks to reduce online recruitment fraud and protect job seekers. 

    </p>
    <hr class="my-8"  />
<h2 class="font-bold">Project Goals</h2> 

 
<ul>
  <li>Build a predictive model to classify job postings as real or fake using a dataset of labeled job postings. </li>
  <li>Analyze which features (textual and numeric) are most indicative of fraudulent intent.</li>
  <li>Develop a pipeline that could be integrated into real-time systems (e.g., job boards or recruitment apps). </li>
  <li>Provide interpretability to help understand why certain jobs are flagged as fake.</li>
  <li>Address class imbalance, a common issue in fraud detection scenarios. </li>
</ul>
<hr class="my-8" />
<h2 class="font-bold">Dataset</h2> 

<p><strong>Name:</strong> Fake Job Postings Dataset</p> 

<p><strong>URL:</strong> <a href="https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction">https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction</a> </p>

<p><strong>Description:</strong> A dataset containing 17,880 rows of job postings with 18 columns of metadata such as job title, location, company profile, requirements, and whether the job is fraudulent. The target column is fraudulent (0 = real, 1 = fake). The dataset can be used to create classification models which can possibly learn which job descriptions are fraudulent. </p>

<p><strong>Size:</strong> 17,880 rows × 18 columns (17,014 real jobs, 866 fake jobs) </p>

<p><strong>Date of Creation:</strong> Uploaded on Kaggle in 2020 </p>

<p><strong>Owner:</strong> Shivam Bansal (via Kaggle) </p>

<p><strong>License:</strong> Public dataset available for non-commercial research </p>

  </div>
</template>

<script setup>

</script>

<style scoped>
h2 {
  font-size: 1.5rem;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}
p {
  margin-bottom: 1rem;
}
ul {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}
li {
  margin-bottom: 0.5rem;
  list-style-type: disc;
}
a {
  color: blue;
  text-decoration: underline;
}
a:hover {
  text-decoration: none;
}

</style>
