<?php
function hashpass($password) {
  return crypt($password, '$2a$07$hyperagressive123jkasdfakrjtwkrjaskfjasdkfjaf$');
}

function get_con() {
  $con = mysql_connect("sql.mit.edu","rcoh","rcoh");
  mysql_select_db("rcoh+gradschool", $con);
  if (!$con)
  {
    die('Could not connect: ' . mysql_error());
  }
  return $con;
}
function query_or_die($query, $con) {
  $result = mysql_query($query, $con);
  if(!$result){
    die('Error: ' . mysql_error());
  } else {
    return $result;
  } 
}

function go_home() {
  header("Location: index.php");
}

function standard_search($query, $con) {
  $stmnt="select distinct prof.id, name, school, department, image from keywords 
    inner join keywordmap on keywords.id=keywordmap.keyword_id 
    join prof on prof.id = keywordmap.prof_id 
    where match (keyword) against ('$query') 
    union select distinct prof.id, name,school, department, image from prof 
    where match(research_summary) against('$query');";
  return query_or_die($stmnt, $con);
}

function prof_by_id($prof_id, $con) {
  $stmnt="select * from prof where id='$prof_id'";
  return query_or_die($stmnt, $con);
}

function research_interests($prof_id, $con) {
  $stmnt = "select distinct keyword from keywords inner join keywordmap on 
    keywords.id=keywordmap.keyword_id join prof 
    on prof.id = keywordmap.prof_id where prof.id=$prof_id;";
  return query_or_die($stmnt, $con);
}
?>

