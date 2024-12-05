<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lake Temperatures</title>
    <!-- Include Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
    <h2 class="mb-4">Lake Temperatures</h2>

    <?php
    $conn = mysqli_connect("pharma.mysql.tools", "pharma_fake", "45dfgthra43", "pharma_fake");
    $user_ip = $_SERVER['REMOTE_ADDR'];
    
    
    // Snoopi API details
    $apikey = "678567-376786-769567956-6796579-30387878";
    $api_url = "https://api.snoopi.io/{$user_ip}?apikey={$apikey}";

    // Fetch the API response
    $response = file_get_contents($api_url);

if ($response !== false) {
    $gpsdata = json_decode($response, true); // Decode JSON response

    // Check if the API returned the required data
    if (isset($gpsdata['Latitude']) && isset($gpsdata['Longitude'])) {
        $latitude = $gpsdata['Latitude'];
        $longitude = $gpsdata['Longitude'];

        // Use the latitude and longitude as needed
//        echo "Visitor Latitude: " . $latitude . "<br>";
//        echo "Visitor Longitude: " . $longitude . "<br>";
    } else {
        echo "Unable to fetch location data.";
    }
} else {
    echo "Failed to connect to the Snoopi API.";
}



    
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Step 1: Extract the MAX(timestamp) from the bavarianlakes table
    $sql1 = "SELECT MAX(timestamp) as max_timestamp FROM bavarianlakes";
    $result1 = $conn->query($sql1);

    // time calcualations starting point
    if ($result1->num_rows > 0) {
    // Fetch the result into an array
    $row = $result1->fetch_assoc();
    $max_timestamp = $row['max_timestamp'];  // e.g., '2024-09-23 15:02:06'

    // Step 2: Calculate how much time ago this timestamp occurred
    $datetime_max = new DateTime($max_timestamp, new DateTimeZone('Europe/Kyiv'));  // Set the correct timezone
    $datetime_now = new DateTime("now", new DateTimeZone('Europe/Kyiv'));           // Current time in Kyiv timezone

    $interval = $datetime_now->diff($datetime_max);  // Calculate the difference

    // Format the time difference as needed (e.g., minutes, hours, days)
    if ($interval->days > 0) {
        $time_ago = $interval->days . " days ago";
    } elseif ($interval->h > 0) {
        $time_ago = $interval->h . " hours ago";
    } elseif ($interval->i > 0) {
        $time_ago = $interval->i . " minutes ago";
    } else {
        $time_ago = "just now";
    }
} else {
    // Handle case where there's no data
    $time_ago = "No data available";
}
    
    
    
    
    // Define the number of results per page
    $results_per_page = 10;

    // Find out the number of results stored in the database
    $result = $conn->query("SELECT COUNT(DISTINCT lake, link) AS total FROM bavarianlakes WHERE timestamp = (SELECT MAX(timestamp) from bavarianlakes)");
    $row = $result->fetch_assoc();
    $total_results = $row['total'];

    // Determine number of total pages available
    $total_pages = ceil($total_results / $results_per_page);

    // Determine which page number visitor is currently on
    $current_page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
    if ($current_page < 1) {
        $current_page = 1;
    } elseif ($current_page > $total_pages) {
        $current_page = $total_pages;
    }

    // Determine the SQL LIMIT starting number for the results on the displaying page
    $starting_limit = ($current_page - 1) * $results_per_page;

    // Retrieve selected results from database and display them on page
     $sql = "SELECT 
            UPPER(bl.lake) as LAKE, 
            bl.link as LINK, 
            bl.temp as CURRENT_TEMP, 
            bl.timestamp as DATETIME, 
            ld.Space, 
            ld.SpaceSpec, 
            ld.MaxDeep, 
            ld.Latitude, 
            ld.Longitude 
        FROM 
            bavarianlakes bl 
        LEFT JOIN 
            lake_convert_data ld 
        ON 
            ld.Link = bl.link 
        WHERE 
            bl.timestamp = (SELECT MAX(timestamp) FROM bavarianlakes) 
        ORDER BY 
            bl.timestamp DESC
        LIMIT $starting_limit, $results_per_page";

    $result = $conn->query($sql);
    ?>

    <table class="table table-striped table-bordered">
        <thead class="thead-dark">
            <tr>
            <th>LAKE</th>
            <th>CURRENT TEMP</th>
            <th>SPACE</th>       <!-- New column -->
            <th>SPACE SPEC</th>  <!-- New column -->
            <th>MAX DEEP</th>    <!-- New column -->
            <th>LATITUDE</th>    <!-- New column -->
            <th>LONGITUDE</th>   <!-- New column -->
            </tr>
        </thead>
        <tbody>
        <?php
        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                echo '<tr>';
                echo '<td><a href="' . $row["LINK"] . '">' . $row["LAKE"] . '</a></td>';
                echo '<td>' . $row["CURRENT_TEMP"] . '</td>';
                echo '<td>' . $row["Space"] . '</td>';       // New column
                echo '<td>' . $row["SpaceSpec"] . '</td>';   // New column
                echo '<td>' . $row["MaxDeep"] . '</td>';     // New column
                echo '<td>' . $row["Latitude"] . '</td>';    // New column
                echo '<td>' . $row["Longitude"] . '</td>';   // New column
                echo '</tr>';
            }
        } else {
            echo '<tr><td colspan="2">No Results</td></tr>';
        }
        $conn->close();
        ?>
        </tbody>
    </table>

    <!-- Pagination -->
    <nav>
        <ul class="pagination justify-content-center">
            <?php
            for ($page = 1; $page <= $total_pages; $page++) {
                $active = ($page == $current_page) ? 'active' : '';
                echo '<li class="page-item ' . $active . '"><a class="page-link" href="index.php?page=' . $page . '">' . $page . '</a></li>';
            }
            ?>
        </ul>
    </nav>
</div>
<!-- Include Bootstrap JS and dependencies -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<h2 class="mb-4" style="font-size: 1.2rem; text-align: center;">Updated <?php echo $time_ago; ?></h2>
<h1 class="mb-4" style="font-size: 0.6rem; text-align: center;">Your IP <?php echo $user_ip; ?></h1>
<h1 class="mb-4" style="font-size: 0.6rem; text-align: center;">
    GPS: 
    <a href="https://www.google.com/maps/search/?api=1&query=<?php echo $latitude . ',' . $longitude; ?>" target="_blank">
        <?php echo $latitude . ' ' . $longitude; ?>
    </a>
</h1>

</body>
</html>
