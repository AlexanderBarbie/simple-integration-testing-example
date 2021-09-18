<test test-name="pubtest" type="publishtest" pkg="rostest">
  <rosparam>
    topics:
      - name: a
        timeout: 1
        negative: False
      - name: b
        timeout: 1
        negative: False
   </rosparam>
  </test>