<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Streamy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
          content="Streamy is a web client for social networks">

    <link rel="shortcut icon" href="/favicon.ico">

    <link rel="stylesheet" href="css/main.css">
    <script src="/static/js/jquery-2.0.2.min.js"></script>
    
  </head>

  <body>

    <section class="redaction"></section>
    
    <section class="feed">
      %for status in enumerate(statuses):

        <article>
          <p>{{ status.author }}</p>
          <p>{{ status.body }}</p>
        </article>

      %end
    </section>

    <footer>
        Streamy - <a href="https://github.com/mart-e/streamy">fork me</a>            
    </footer>

  </body>

</html>
